from tkinter import Tk, Frame, Button, Canvas, BOTH, RIGHT, CENTER, LEFT, X, Y
import docker

docker_client = docker.from_env()

class Window(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master
        self.master.title('Build and Run')

        Button(self, text='Run Data Pipeline', command=self._run_data_pipeline).pack(fill=X, padx=10, pady=10)
        Button(self, text='Run Trainng Locally', command=self._run_training_locally).pack(fill=X, padx=10, pady=10)
        Button(self, text='Run Batch Predictions', command=self._batch_predict).pack(fill=X, padx=10, pady=10)

        Button(self, text='Build Training Docker', command=self._build_training_docker).pack(fill=X, padx=10, pady=10)
        Button(self, text='Build Predicting Docker', command=self._build_predict_docker).pack(fill=X, padx=10, pady=10)

        Button(self, text='Run Training Docker', command=self._run_training_docker).pack(fill=X, padx=10, pady=10)
        Button(self, text='Run Predicting Server', command=self._run_predict_server).pack(fill=X, padx=10, pady=10)

        Button(self, text='Predict Locally', command=self._predict_locally).pack(fill=X, padx=10, pady=10)
        Button(self, text='Predict on Docker Server', command=self._predict_with_docker).pack(fill=X, padx=10, pady=10)
        Button(self, text='Predict on SageMaker', command=self._predict_with_sagemaker).pack(fill=X, padx=10, pady=10)

        Button(self, text='Quit', command=self.client_exit).pack(fill=X, padx=10, pady=10)
        self.pack(fill=BOTH)

    def _run_data_pipeline(self):
        print('run data pipeline ...')

    def _run_training_locally(self):
        print('run local training ...')

    def _batch_predict(self):
        print('run batch predictions ...')

    def _build_training_docker(self):
        print('building training docker ...')
        for image in docker_client.images.list():
            print(image.attrs)

    def _build_predict_docker(self):
        print('building predicting docker ...')

    def _run_training_docker(self):
        print('run training docker ...')
        for container in docker_client.containers.list(all=True):
            print(container.attrs)
            container.remove()

    def _run_predict_server(self):
        print('run predicting server ...')

    def _predict_locally(self):
        print('run predict locally ...')

    def _predict_with_docker(self):
        print('run predict with docker server ...')

    def _predict_with_sagemaker(self):
        print('run predict with sagemaker ...')

    def client_exit(self):
        exit(0)

root = Tk()
root.geometry('400x500+200+200')
app = Window(root)
root.mainloop()
