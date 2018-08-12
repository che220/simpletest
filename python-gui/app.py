from tkinter import *
from tkinter import messagebox
from tkinter.ttk import Combobox
import docker

root = Tk()
docker_client = docker.from_env()

class SageMakerParamDialog:
    def __init__(self, parent):
        self.top = Toplevel(parent)
        self.mxs_env = self.mxs_version = None
        self.cancelled = False

        canvas = Canvas(self.top, highlightthickness=0)
        canvas.pack(fill=X, expand=1, padx=10)
        for i in range(4):
            Grid.rowconfigure(canvas, i, weight=1)
        for i in range(2):
            Grid.columnconfigure(canvas, i, weight=1)

        row = 0
        Label(canvas, text='MXS Env:').grid(row=row, column=0, sticky=N+S+E+W, padx=10, pady=10)
        self.env_combo = Combobox(canvas, state='readonly', value=['cdev', 'e2e', 'cperf', 'prod'])
        self.env_combo.current(1)
        self.env_combo.grid(row=row, column=1)

        row += 1
        Label(canvas, text='MXS Major Version:').grid(row=row, column=0, sticky=N+S+E+W, padx=10, pady=10)
        self.version_entry = Entry(canvas)
        self.version_entry.grid(row=row, column=1, sticky=N+S+E+W, padx=10, pady=10)

        row += 1
        Button(canvas, text='Cancel', command=self._cancel).grid(row=row, column=0, sticky=N+S+E+W, padx=10, pady=10)
        Button(canvas, text='OK', command=self._ok).grid(row=row, column=1, sticky=N+S+E+W, padx=10, pady=10)
        root.wait_window(self.top)

    def _cancel(self):
        self.cancelled = True
        self.top.destroy()

    def _ok(self):
        self.mxs_env = self.env_combo.get()
        self.mxs_version = self.version_entry.get()
        self.top.destroy()

class Window(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master
        self.master.title('Build and Run')

        Button(self, text='Run Data Pipeline', command=self._run_data_pipeline).pack(fill=X, padx=10, pady=10)

        canvas = Canvas(self, highlightthickness=0)
        canvas.pack(fill=X, expand=1, padx=10)
        for i in range(4):
            Grid.rowconfigure(canvas, i, weight=1)
        for i in range(2):
            Grid.columnconfigure(canvas, i, weight=1)

        row = 0
        Button(canvas, text='Build Docker', command=self._build_docker).grid(row=row, column=0, sticky=N+S+E+W, padx=10, pady=10)
        self.docker_combo = Combobox(canvas, state='readonly', value=['for training', 'for predicting'])
        self.docker_combo.current(0)
        self.docker_combo.grid(row=row, column=1)

        row += 1
        Button(canvas, text='Run Trainng', command=self._run_training).grid(row=row, column=0, sticky=N+S+E+W, padx=10, pady=10)
        self.train_combo = Combobox(canvas, state='readonly', value=['locally', 'with docker'])
        self.train_combo.current(0)
        self.train_combo.grid(row=row, column=1)

        row += 1
        btn = Button(canvas, text='Run Predicting Docker Server', command=self._run_predict_server)
        btn.grid(row=row, column=0, columnspan=2, sticky=N+S+E+W, padx=10, pady=10)

        row += 1
        Button(canvas, text='Run Predictions', command=self._run_predict).grid(row=row, column=0, sticky=N+S+E+W, padx=10, pady=10)
        self.predict_combo = Combobox(canvas, state='readonly', value=['in batch', 'on docker server', 'on AWS SageMaker'])
        self.predict_combo.current(0)
        self.predict_combo.grid(row=row, column=1)

        Button(self, text='Exit', command=self._client_exit).pack(fill=X, padx=10, pady=10)
        self.pack(fill=BOTH)

    def _run_data_pipeline(self):
        print('run data pipeline ...')

    def _run_training(self):
        val = self.train_combo.get()
        print('run training {} ...'.format(val))
        if 'docker' in val:
            self._list_and_remove_containers()

    def _run_predict(self):
        val = self.predict_combo.get()
        print('run prediction(s) {} ...'.format(val))
        if 'docker' in val:
            self._list_and_remove_containers()
        elif 'SageMaker' in val:
            dialog = SageMakerParamDialog(self)
            if dialog.cancelled:
                return

            env = dialog.mxs_env
            version = dialog.mxs_version
            print('run tests against sagemake with mxs env = {} and mxs verion = {}'.format(env, version))

    def _build_docker(self):
        val = self.docker_combo
        print('building docker {} ...'.format(val))
        self._list_images()

    def _run_predict_server(self):
        print('run predicting server ...')

    def _client_exit(self):
        if messagebox.askyesno("Please Verify", "Do you really want to exit?"):
            exit(0)

    def _list_and_remove_containers(self):
        for container in docker_client.containers.list(all=True):
            print(container.attrs)
            container.remove()

    def _list_images(self):
        for image in docker_client.images.list():
            print(image.attrs)

if __name__ == '__main__':
    root.geometry('400x300+0+0')
    app = Window(root)
    root.mainloop()
