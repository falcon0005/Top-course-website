import React, { useEffect } from "react";
import {apiUrl,filterData} from "./data.js";
import Navbar from "./components/Navbar";
import Cards from "./components/Cards";
import Filter from "./components/Filter";
import {toast} from "react-toastify";
import {useState} from "react";
import Spinner from "./components/Spinner.js";
 
const App = () => {
  const[courses,setCourses]=useState(null);
  const[loading,setLoading]=useState(true);
  const[category,setCategory]=useState(filterData[0].title);
    async function fetchData(){
      setLoading(true);
      try{
        let res=await fetch(apiUrl);
        let output=await res.json();
        //save data into a variable
        setCourses(output.data);
      }
      catch(error){
        toast.error("Something went wrong");
      }
      setLoading(false);
    }
    useEffect(()=>{
      fetchData();
    },[])

  return(
    <div className="min-h-screen flex flex-col bg-bgDark2">
      <div>
      <Navbar></Navbar>
      </div>
      <div className="bg-bgDark2">
      <div>
      <Filter filterData={filterData} category={category} setCategory={setCategory}></Filter>
      </div>
      <div className="w-11/12 max-w-[1200px] 
        mx-auto flex flex-wrap justify-center items-center min-h-[50vh]">
        {
          loading?(<Spinner/>):(<Cards courses={courses} category={category}></Cards>)
        }
      </div>  
      </div>
    </div>
  )
};

export default App;
