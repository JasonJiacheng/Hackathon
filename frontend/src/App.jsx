import { Routes, Route } from "react-router-dom"; 
import Home from "./pages/Home"; 
import Generate from "./pages/Generate"; 
import Library from "./pages/Library"; 
import Outfits from "./pages/Outfits"; 
import Upload from "./pages/Upload"; 

 

function App() { 
    return( 
      <Routes> 
        <Route path="/" element={<Home />} /> 
        <Route path="/Generate" element={<Generate />} /> 
        <Route path="/Library" element={<Library />} /> 
        <Route path="/Outfits" element={<Outfits />} /> 
        <Route path="/Upload" element={<Upload />} /> 
      </Routes> 
    ); 
} 

 

export default App; 