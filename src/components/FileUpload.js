
import axios from 'axios'; 
import "./global.css";  
import React,{Component} from 'react'; 
  
class App extends Component { 
   
    state = { 
  
      // Initially, no file is selected 
      selectedFile: null
    }; 
     
    // On file select (from the pop up) 
    onFileChange = event => { 
     
      // Update the state 
      this.setState({ selectedFile: event.target.files[0] }); 
     
    }; 

    
     
    // On file upload (click the upload button) 
    onFileUpload = () => { 
     
      // Create an object of formData 
      const formData = new FormData(); 
     
      // Update the formData object 
      formData.append( 
        "myFile", 
        this.state.selectedFile, 
        this.state.selectedFile.name 
      ); 
     
      // Details of the uploaded file 
      console.log(this.state.selectedFile); 
     
      // Request made to the backend api 
      // Send formData object 
      axios.post("api/uploadfile", formData); 
      window.location.href="/postlogin/viewresults";
    }; 
     
    // File content to be displayed after 
    // file upload is complete 
    fileData = () => { 
     
      if (this.state.selectedFile) { 
          
        return ( 
          <div> 
            <h2>File Details:</h2> 
            <p>File Name: {this.state.selectedFile.name}</p> 
            <p>File Type: {this.state.selectedFile.type}</p> 
          </div> 
        ); 
      } else { 
        return ( 
          <div> 
            <br /> 
            <h4>Choose before Pressing the Upload button</h4> 
          </div> 
        ); 
      } 
    }; 

    
     
    render() { 

      function changeColor(e) {
        e.target.style.background = '#4682B4';
      }
      
      function defaultColor(e){
        e.target.style.background = ' rgb(20, 16, 56)';
      }
     
      return ( 
        <div class="uploadcontainer"> 
            <h1> 
              Upload your files in a zip file
            </h1> 
            <div class="browse"> 
                <input type="file" style={{width: "20%"}}onChange={this.onFileChange} /> <br />
                <button onClick={this.onFileUpload} style={{height: "50px"}} onMouseOver={changeColor} onMouseLeave={defaultColor}> 
                  Upload file
                </button> 
            </div> 
          {this.fileData()} 
        </div> 
      ); 
    } 
  } 
  
  export default App; 
