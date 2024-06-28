import { Route, Routes } from "react-router-dom";
import HomeScreen from "./Screens/HomeScreen";
import Aos from "aos";
import Role from "./Screens/Role";
import UploadCSV from "./Screens/DashBoard/UploadCSV";
import Details from "./Screens/DashBoard/Details";
import Performance from "./Screens/DashBoard/Performance";
import Download from "./Screens/DashBoard/Download";


function App() {
  Aos.init();
  return (
    <>
      <Routes>
        <Route path="/" element={<HomeScreen />} />
        <Route path="/role" element={<Role />} />
        <Route path="/upload_csv" element={<UploadCSV />} />
        <Route path="/details" element={<Details />} />
        <Route path="/performance" element={<Performance />} />
        <Route path="/download" element={<Download />} />
      </Routes>
    </>
  )
}

export default App
