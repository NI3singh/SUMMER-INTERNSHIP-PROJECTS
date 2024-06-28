import NavBar from "./NavBar/NavBar";
import Footer from "./Footer/Footer";

// Layout component to wrap the main content of the application with a NavBar and Footer
function Layout({ children }) {
  return (
    <>
      <div className="bg-white">
        <NavBar />
        {/* Main content passed as children */}
        {children}
        <Footer />
      </div>
    </>
  );
}

export default Layout;
