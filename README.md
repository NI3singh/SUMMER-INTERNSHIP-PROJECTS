# 🚀 Student Performance Analysis Project 📊

This project analyzes student performance data to identify trends, cluster students based on their performance, and provide actionable insights into their academic progress.  It leverages Python for data processing and analysis, and a React-based web interface for user interaction.

## 📚 Table of Contents

- [🎯 Project Goals](#project-goals)
- [🛠️ Technologies Used](#technologies-used)
- [⚙️ Setup (Backend - Python)](#setup-backend-python)
- [💻 Setup (Frontend - React)](#setup-frontend-react)
- [💡 Usage](#usage)
    - [📂 File Upload](#file-upload)
    - [🧑‍🎓 Student Details](#student-details)
    - [📈 Performance Analysis](#performance-analysis)
    - [⬇️ Download Data](#download-data)
- [🧮 Data Processing (Python)](#data-processing-python)
    - [💾 Data Extraction](#data-extraction)
    - [🧹 Data Preparation](#data-preparation)
    - [✨ Data Transformation](#data-transformation)
    - [📊 Exploratory Data Analysis (EDA)](#exploratory-data-analysis-eda)
    - [🤖 Modeling](#modeling)
    - [📈 Evaluation](#evaluation)
- [🖼️ Screenshots](#screenshots)
- [✨ Future Enhancements](#future-enhancements)
- [🤝 Contributing](#contributing)
- [📄 License](#license)

## 🎯 Project Goals

- Identify trends in student performance over time.
- Cluster students into performance groups (e.g., Strong, Average, Weak).
- Provide a user-friendly web interface for data upload, analysis, and visualization.
- Generate reports that can be used by educators and administrators.

## 🛠️ Technologies Used

**Backend (Python):**

-   🐍 Python
-   🐼 Pandas
-   🔢 NumPy
-   📈 Matplotlib
-   📊 Seaborn
-   🤖 Scikit-learn

**Frontend (React):**

-   ⚛️ React
-   🗺️ React Router
-   🎨 Material UI (MUI X Charts, Typography)
-   🔗 Axios
-   ⬇️ js-file-download
-   🔤 react-icons
-   ✨ AOS (for animations)
-   🌈 Tailwind CSS

## ⚙️ Setup (Backend - Python)

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/rishabhamar/student-performance-analysis
    ```
2.  **Navigate to the project directory:**
    ```bash
    cd student-performance-analysis/backend  # Go to the backend directory
    ```
3.  **Create a virtual environment (recommended):**
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Linux/macOS
    venv\Scripts\activate  # On Windows
    ```
4.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
5.  **Run the backend:** 
    ```bash
    python app.py
    ```

## 💻 Setup (Frontend - React)

1.  **Navigate to the frontend directory:**
    ```bash
    cd student-performance-analysis/frontend
    ```
2.  **Install dependencies:**
    ```bash
    npm install
    # or
    yarn install
    ```
3.  **Start the development server:**
    ```bash
    npm start
    # or
    yarn start
    ```
    This will start the development server and open the application in your browser.

## 💡 Usage

### 📂 File Upload

-   Upload CSV files containing student data (train, test, or combined).
### 🧑‍🎓 Student Details

-   View individual student profiles, including enrollment number, name, and division.

### 📈 Performance Analysis

-   Analyze student performance by subject.
-   View trends over time using line charts.
-   Compare performance against class averages.
-   Use filters to select specific subjects.
-   Visualize class performance breakdown using pie charts.

### ⬇️ Download Data

-   Download the processed data in Excel format.

## 🧮 Data Processing (Python)

### 💾 Data Extraction

-   Data is loaded from CSV files using Pandas.

### 🧹 Data Preparation

-   Handling missing values (imputation or removal).
-   Data type conversion.
-   Feature identification (numerical and categorical).

### ✨ Data Transformation

-   Feature scaling (e.g., StandardScaler).
-   Feature engineering.

### 📊 Exploratory Data Analysis (EDA)

-   Visualizations (histograms, box plots, scatter plots).
-   Statistical summaries.
-   Correlation analysis.

### 🤖 Modeling

-   Clustering algorithms (e.g., K-Means, Agglomerative Clustering).

### 📈 Evaluation

-   Performance metrics (e.g., silhouette score).
-   Trend analysis.

## 🖼️ Screenshots

### 1. Intro Page
![Intro Page Screenshot](https://github.com/user-attachments/assets/ee6ff758-faf2-4e09-b7bf-0ebd9c35838d)
*A welcoming introduction to the Student Performance Analysis web app.*

### 2. Role Selection
![Role Selection Screenshot](https://github.com/user-attachments/assets/62c91309-ba92-4ae4-8ea1-20b6419f1191)
*Users can select their role (Student, Teacher, or Admin).*

### 3. File Upload
![File Upload Screenshot](https://github.com/user-attachments/assets/31f12ee2-9e08-4402-be9b-15e20126cf83)
*Uploading student data in CSV format.*

![File Upload Screenshot](https://github.com/user-attachments/assets/e5b0885a-2080-402d-8c1d-e4306e4df412)
*Viewing individual student profiles and information.*

### 4. Performance Analysis - Overview
![Performance Analysis Overview Screenshot](https://github.com/user-attachments/assets/43180b06-ae94-4791-bdc1-e8bf00a13fe9)


![Performance Analysis Subject Screenshot](https://github.com/user-attachments/assets/0654361a-039b-465f-9574-a0c5d066c814)
*A summary of student performance across subjects.*

### 5. Download Data
![Performance Analysis Trend Screenshot](https://github.com/user-attachments/assets/0a5b3e79-515f-4cfc-9017-374e4bc66953)
*Visualizing student performance trends over time.*

## 📽️ Video

https://github.com/user-attachments/assets/07626685-19d2-4f1b-804c-78fb2ada77fb

## ✨ Future Enhancements

-   **Backend Integration:** Fully integrate the frontend with a robust backend.
-   **User Authentication:** Implement secure user authentication based on roles (Student, Teacher, Admin).
-   **Improved UI/UX:** Enhance the user interface and user experience based on user feedback.
-   **Interactive Charts:** Make the charts more interactive and customizable.
-   **More Detailed Analysis:** Provide more in-depth performance analysis options, such as percentile rankings, subject-specific insights, and predictive modeling.
-   **Data Validation:** Add robust data validation for uploaded CSV files to prevent errors.
-   **Reporting:** Generate automated reports for teachers and administrators.

## 🤝 Contributing

Contributions are welcome! Please open an issue or submit a pull request.

## 📄 License

[Choose a license for your project (e.g., MIT, Apache 2.0)]
