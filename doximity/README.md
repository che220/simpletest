# Doximity's Data Scientist Assignment
##### Proprietary and Confidential
------------

You are working for a large marketing firm that targets doctors based on their practice area. Your current campaign is targeting Cardiologists, and you are tasked with coming up with a list of doctors to contact.

You are given a file, **`physicians.csv`**, which contains a list of doctors and their unique specialty. You notice that there are a decent number of doctors with "Cardiology" as a specialty, but there are also quite a few doctors whose specialty is "Unknown". You wonder if any of these doctors might actually be Cardiologists.

You find a public dataset, **`procedures.csv`**, which contains a list of procedures your doctors performed over the past year.
The columns of this dataset are as follows:

* **`physician_id`** unique physician identifier, joins to `id` in **`physicians.csv`**
* **`procedure_code`** unique code representing a procedure
* **`procedure`** description of the procedure performed
* **`number_of_patients`** the number of patients the doctor performed that procedure on over the past year

------------

Using these procedure data, determine whether the pool of cardiologists can be increased. Down the road, the marketing firm may want to classify physicians under medical specialties other than cardiology (e.g., anesthesiology, neurology). Consider building a model for finding cardiologists as a first step toward this and advise on whether this approach may be reused for discerning these other specialties as well.

Both files can be found in this repository. Please submit all relevant code and write a detailed explanation of your methodology and results. Assume both a data scientist and a product manager will look over your results. We’re a Python shop - feel free to use any libraries you see fit.

------------

## Submission instructions

1. Provide your Doximity point of contact with your GitLab username (create a new account if you do not already have one). Your point of contact will add you to the data challenge repository. Once you've been added to the repo, you should see in the Project tab the `data-science` project containing the challenge instructions.
2. Fork the `data-science` repository.
3. In the `data-science` project tab, click on `Members`. Under `Project members`, click on the `Add member` tab. Under `Select members to invite`, please type in `Doximity-data` and choose the `Developer` role permission. When done, click `Add to project`. This will enable us to review your challenge submission (turned in as a `Merge Request`) when complete.
4. In the forked `data-science` project, create a new branch `lastname-firstname`. Work on the assignment and commit your changes to the `lastname-firstname` branch.
5. When complete with the assignment, after having commit all your changes, create a new `Merge Request`. Add `Doximity-data` as an assignee, so we are notified you have submit the `Merge Request`. We will then review your submission and get back to you.

* For a visual walk-through of the submission process, please watch [this video](https://vimeo.com/227828054/562c3f6acf). 
* If any questions come up, please send an email to your Doximity point of contact.