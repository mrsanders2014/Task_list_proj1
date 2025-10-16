import React from 'react';
import Navbar from './Navbar';
import Footer from './Footer';

const MainLayout = ({ children, showFooter = true }) => {
  return (
    <div className="min-h-screen bg-gray-50 flex flex-col">
      <Navbar />
      <main className="flex-1">
        {children}
      </main>
      {showFooter && <Footer />}
    </div>
  );
};

export default MainLayout;
