import SideBar from "./SideBar";
import { LineChart } from "@mui/x-charts/LineChart";
import { PieChart, pieArcLabelClasses } from "@mui/x-charts/PieChart";
import Typography from "@mui/material/Typography";
import { useState } from "react";
import axios from "axios";
import { FaFilter } from "react-icons/fa";

function Performance() {
  // State variables
  const [enr, setEnr] = useState(""); // Enrollment number input
  const [data, setData] = useState(""); // Data fetched from the server
  const [filt, setFilt] = useState(0); // Filter flag

  // Handle enrollment number input change
  const handleInput = (event) => {
    setEnr(event.target.value);
  };

  // Handle form submission to send enrollment number to the server
  const handleSubmit = (event) => {
    event.preventDefault();
    const url = "https://student-performance-analysis-7du3.onrender.com/data";
    console.log(enr);
    const data = { enrollment: enr };
    const config = {
      headers: {
        "Content-Type": "application/json",
      },
    };
    axios
      .post(url, data, config)
      .then((response) => console.log(response))
      .catch((err) => console.log(err));
    setFilt(0);
  };

  // Fetch data from the server
  const fetchData = async () => {
    try {
      const result = await axios.get("https://student-performance-analysis-7du3.onrender.com/fetch_data");
      console.log(result);
      console.log(result.data);
      setData(result.data);
      setFilt(0);
    } catch (err) {
      console.log(err);
    }
  };

  // Sample data for line chart
  const xAxisData = [
    "Term 1 2019",
    "Term 2 2019",
    "Term 3 2019",
    "Term 1 2020",
    "Term 2 2020",
    "Term 3 2020",
  ];
  const seriesData = [55.0, 62.5, 72.5, 63.0, 90.3, 80.0];

  // Additional state variables for subject filtering
  const [value, setValue] = useState("");
  const [subjectList, setSubjectList] = useState([
    "Overall",
    "Math",
    "Science",
    "English",
  ]);
  const [subjectList1, setSubjectList1] = useState(subjectList);
  const [subject, setSubject] = useState("");
  const [sub, setSub] = useState("");

  // Handle filter input change
  const filterEvent = (e) => {
    console.log(e.target.value);
    setValue(e.target.value);
    if (e.target.value) {
      let result = subjectList1.filter((item) =>
        item.toLowerCase().includes(e.target.value.toLowerCase()),
      );
      console.log(result);
      setSubjectList(result);
    } else {
      setSubjectList(subjectList1);
    }
    setFilt(0);
  };

  // Apply filter based on selected subject
  const filter = () => {
    if (subjectList[0] === "Overall") {
      setSubject("");
    } else {
      setSubject(subjectList[0]);
    }
    setSub(subjectList[0]);
    setFilt(1);
    console.log(subject);
    console.log(`${subject} Performance`);
    console.log(`${subject} Improvement Status`);
  };

  return (
    <SideBar>
      {/* Enrollment number form */}
      <div className="grid p-3 items-end">
        <form onSubmit={handleSubmit} className="mx-full">
          <input
            type="number"
            onChange={handleInput}
            id="enr"
            className="mx-auto justify-end rounded-sm"
            placeholder="Enter Enrollment No."
            value={enr}
          />
          <button type="submit" className="text-white bg-star w-1/6 rounded-sm">
            Submit
          </button>
        </form>
      </div>
      {/* Fetch performance button */}
      <div className="grid p-3 items-end">
        <button
          onClick={fetchData}
          className="text-white bg-star w-1/6 rounded-sm"
        >
          Check Performance
        </button>
      </div>
      {/* Performance heading */}
      <div className="text-white font-bold text-3xl text-center border-4 border-b-2 border-white p-3">
        Check Performance
      </div>
      {/* Subject filter input and button */}
      <div className="flex flex-row p-2 w-1/5">
        <div className="flex p-1">
          <input
            value={value}
            onChange={(e) => filterEvent(e)}
            list="subject"
            placeholder="Filter Subject"
            className="p-2 rounded"
          />
        </div>
        <div className="flex p-1">
          <button
            className="bg-subMain w-20 flex-colo h-12 rounded text-white"
            onClick={() => filter()}
          >
            Filter <FaFilter />
          </button>
        </div>
        <div className="flex p-2">
          {filt === 1 ? (
            <p className="text-white p-2 bg-star justify-center rounded-lg">
              {sub}
            </p>
          ) : null}
        </div>
      </div>
      <div>
        <datalist id="subject">
          {subjectList.map((item, index) => (
            <option key={index}>{item}</option>
          ))}
        </datalist>
      </div>
      {/* Performance and trend display */}
      <div className="grid sm:grid-cols-2 lg:grid-cols-2 gap-6 m-4 justify-center">
        <div className="flex justify-center text-white text-lg">
          <div className="col-span-3">
            <h1>{sub} Performance</h1>
            {!data ? (
              <p className="text-center">Loading...</p>
            ) : (
              <p className="text-center">
                {data[`${subject} Performance`.trim()]
                  ? data[`${subject} Performance`.trim()][0]
                  : "No performance data available"}
              </p>
            )}
          </div>
        </div>
        <div className="flex justify-center text-white text-lg">
          <div className="col-span-3">
            <h1>{sub} Trend</h1>
            {!data ? (
              <p className="text-center">Loading...</p>
            ) : (
              <p className="text-center">
                {data[`${subject} Improvement Status`.trim()]
                  ? data[`${subject} Improvement Status`.trim()][0]
                  : "No Improvement Status data available"}
              </p>
            )}
          </div>
        </div>
      </div>
      {/* Line chart for performance trend */}
      <div className="flex bg-white w-auto rounded-lg p-5 justify-center">
        <div className="text-main text-xl text-center">{sub} Trend</div>
        <LineChart
          xAxis={[
            {
              scaleType: "band",
              data:
                filt === 0
                  ? xAxisData
                  : data[`feature_${subject.toLowerCase()}`],
            },
          ]}
          series={[
            {
              name: "Performance",
              data:
                filt === 0
                  ? seriesData
                  : data[`feature_${subject.toLowerCase()}`].map(
                      (term) => data[term],
                    ),
              type: "line",
              smooth: true,
            },
          ]}
          width={750}
          height={500}
        />
      </div>
      {/* Class performance heading */}
      <div className="text-white p-10 text-xl text-center">
        Class Performance
      </div>
      {/* Pie chart for class performance */}
      <div className="flex bg-white w-auto rounded-lg p-5 justify-center">
        <Typography>{sub} Class Performance</Typography>
        <PieChart
          series={[
            {
              arcLabel: (item) => `${item.label} (${item.value})`,
              data:
                filt === 0
                  ? [
                      { id: 0, value: 100, label: "Strong" },
                      { id: 1, value: 200, label: "Average" },
                      { id: 2, value: 150, label: "Weak" },
                    ]
                  : Object.entries(
                      data[`clusters_${subject.toLowerCase()}`],
                    ).map(([key, value], index) => ({
                      id: index,
                      value: value,
                      label: key,
                    })),
              paddingAngle: 2,
              cornerRadius: 10,
              innerRadius: 3,
              highlightScope: { faded: "global", highlighted: "item" },
              faded: { innerRadius: 30, additionalRadius: -30, color: "gray" },
            },
          ]}
          sx={{
            [`& .${pieArcLabelClasses.root}`]: {
              fill: "white",
              fontWeight: "bold",
            },
          }}
          width={700}
          height={500}
        />
      </div>
    </SideBar>
  );
}

export default Performance;
