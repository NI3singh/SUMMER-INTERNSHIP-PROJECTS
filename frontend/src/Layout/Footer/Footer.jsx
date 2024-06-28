import { Link } from "react-router-dom";

// Footer component for displaying footer content and links
function Footer() {
  return (
    <div className="bg-main py-4 border-t-2 border-black">
      <div className="container mx-auto px-10">
        {/* Grid layout for organizing footer content */}
        <div className="grid grid-cols-2 md:grid-cols-7 xl:grid-cols-12 gap-10 sm:gap-9 lg:gap-11 xl:gap-7 py-10 justify-top">
          {/* Logo and contact information section */}
          <div className="pb-3.5 sm:pb-0 col-span-1 md:col-span-2 lg:col-span-3">
            <Link to="/">
              <img
                src="/site-logo-white-2.png"
                alt="logo"
                className="w-2/4 object-contain h-30"
              />
            </Link>
            {/* Contact information */}
            <p className="leading-7 text-sm text-border mt-3">
              <span>
                Lorem 196 Andrew Road, Suite 200, <br /> New York, NY 10007
              </span>
              <br />
              <span>Tell: 0000000000</span>
              <br />
              <span>Email: demo@email.com</span>
            </p>
          </div>
          {/* Additional sections can be added for more links or content */}
        </div>
      </div>
    </div>
  );
}

export default Footer;
