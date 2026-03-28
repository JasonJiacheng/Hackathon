import './App.css'
import { Routes, Route } from "react-router-dom";
import Home from "./pages/Home";
import Generate from "./pages/Generate";
import Library from "./pages/Upload";
import Outfits from "./pages/Outfits";
import Upload from "./pages/Library";

function App() {
    return(
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/GenerateOutfit" element={<Generate />} />
        <Route path="/UploadedImages" element={<Library />} />
        <Route path="/Outfits" element={<Outfits />} />
        <Route path="/Upload" element={<Upload />} />
      </Routes>
    );

}

export default App;
