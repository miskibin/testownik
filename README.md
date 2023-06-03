# tester app

Simple app for taking quizzes. You can create your own quizzes. 

# Installation 
1. Download app from release page
2. download [combined.txt](./combined.txt) file and put it in the same directory as main app.


## example images of app. 
![image](https://user-images.githubusercontent.com/77834536/215347079-8acd6ec9-aca5-4d38-9a88-ef96504f41b9.png)
![image](https://user-images.githubusercontent.com/77834536/215347136-4d7f408b-ea34-4603-9666-159ff390f6c5.png)
![image](https://user-images.githubusercontent.com/77834536/215347174-25175700-591c-4c19-ad55-7cf6ada83737.png)
![image](https://user-images.githubusercontent.com/77834536/215347312-5f143731-eaf4-46ba-83b8-e22712bc81e1.png)

# Features

## Question and Answer Quiz:

- Users can take a quiz consisting of multiple-choice questions.
- Each question has a question statement and multiple answer options.
- Users can select one answer option as their response.
- The correct answer is indicated with a checkmark symbol (✔️).
- If the user selects an incorrect answer, it is indicated with a cross symbol (❌).

## Question Generation:

- Questions and answers are loaded from a file named "combined.txt".
- The file follows a specific format to define questions, answers, and correct answers.

## Randomized Question Selection:

- The application randomly selects a specified number of questions from the available question pool.
- Users can configure the number of questions for each quiz session.

## Progress Tracking:

- The application keeps track of the user's progress.
- Each question tracks the number of times it has been attempted and the number of times it has been answered correctly.
- Questions are considered "mastered" when the user has answered them correctly more than 70% of the time after at least two attempts.

## User Interface:

- The application provides a graphical user interface (GUI) for a better user experience.
- Questions and answer options are displayed in a visually appealing layout.
- Users can select answers using checkboxes and submit their responses.
- Progress statistics, including the number of mastered questions, total attempts, and overall progress, are displayed in the footer.

## Dialogs and Notifications:

- The application displays informative dialogs for correct and incorrect answers.
- A dialog is also shown when the user finishes the quiz.
