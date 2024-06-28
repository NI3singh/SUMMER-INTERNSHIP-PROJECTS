import { Link } from "react-router-dom";

function NavBar() {
  return (
    <>
      <div className="bg-main shadow-md sticky top-0 z-20 flex items-center">
        <div className="container mx-15 py-3 px-10 lg:grid gap-20 grid-cols-8 justify-between items-center ">
          {/* Logo */}
          <div className="col-span-2 lg:block hidden px-5">
            <Link to="/">
              <img
                src="/site-logo-white-2.png"
                alt="logo"
                className="w-30 h-15 object-cotain"
              />
            </Link>
          </div>
        </div>
      </div>
    </>
  );
}

export default NavBar;
