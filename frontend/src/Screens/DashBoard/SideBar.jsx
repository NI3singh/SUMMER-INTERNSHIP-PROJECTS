import {
    FaCloudDownloadAlt,
    FaCloudUploadAlt,
    FaListAlt,
  } from "react-icons/fa";
  import { CgPerformance } from "react-icons/cg";
  import Layout from "../../Layout/Layout";
  import { NavLink } from "react-router-dom";
  
  function SideBar({ children }) {
    // Array of sidebar links with their respective names, routes, and icons
    const SideLinks = [
      {
        name: "Upload CSV",
        link: "/upload_csv",
        icon: FaCloudUploadAlt,
      },
      {
        name: "Details",
        link: "/details",
        icon: FaListAlt,
      },
      {
        name: "Check Performance",
        link: "/performance",
        icon: CgPerformance,
      },
      {
        name: "Download",
        link: "/download",
        icon: FaCloudDownloadAlt,
      },
    ];
  
    // Classes for active, hover, and inactive link states
    const active = "bg-dryGray text-main";
    const hover = "hover:text-main hover:bg-white";
    const inActive =
      "rounded font-medium text-sm transitions flex gap-3 items-center p-4";
  
    // Function to set the appropriate class based on the active state
    const Hover = ({ isActive }) =>
      isActive ? `${active} ${inActive}` : `${inActive} ${hover}`;
  
    return (
      <Layout>
        <div className="min-h-screen container mx-auto px-2">
          <div className="xl:grid grid-cols-10 gap-5 items-start md:py-12 py-6">
            {/* Sidebar section */}
            <div className="col-span-2 sticky bg-main border border-gray-800 p-5 rounded-md xl:mb-0 mb-5 text-white">
              {
                // Rendering sidebar links
                SideLinks.map((link, index) => (
                  <NavLink to={link.link} key={index} className={Hover}>
                    <link.icon /> <p>{link.name}</p>
                  </NavLink>
                ))
              }
            </div>
            {/* Content section */}
            <div
              data-aos="fade-up"
              data-aos-duration="1000"
              data-aos-delay="10"
              data-aos-offset="200"
              className="col-span-8 rounded-md bg-main border border-gray-800 p-6"
            >
              {children}
            </div>
          </div>
        </div>
      </Layout>
    );
  }
  
  export default SideBar;
  