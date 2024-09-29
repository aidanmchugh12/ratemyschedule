// import React from "react";
// import { withRouter } from "react-router-dom";

// class InputData extends React.Component {
//   constructor() {
//     super();
    
//     this.state = {
//       classNames: [],
//       classProfs: Array(5).fill(''),
//       classCredits: Array(5).fill(1),
//     };
//   }

//   getDataFromBackend = async () => {
//     const response = await fetch('http://127.0.0.1:5000/api/input');
//     const data = await response.json();
//     this.setClassNames(data);
//   }

//   postDataToBackend = async () => {
//     const data = {
//       classes: [this.state.classNames, this.state.classProfs, this.state.classCredits]
//     }
  
//     try {
//       const response = await fetch('http://127.0.0.1:5000/api/input', {
//         method: 'POST',
//         headers: {
//           'Content-Type': 'application/json',
//         },
//         body: JSON.stringify(data),
//       });
  
//       if (!response.ok) {
//         throw new Error('Network response was not ok');
//       }
  
//       const result = await response.json();
//       console.log(result);

//       this.props.history.push('/output');
//     } catch (error) {
//       console.error('Error:', error);
//     }
//   };

//   handleProfessorChange = (index, event) => {
//     const newProfs = [...this.state.classProfs];
//     newProfs[index] = event.target.value;
//     this.setState({ classProfs: newProfs });
//   }

//   handleCreditChange = (index, event) => {
//     const newCredits = [...this.state.classCredits];
//     newCredits[index] = Number(event.target.value);
//     this.setState({ classCredits: newCredits });
//   }

//   handleSubmit = () => {
//     // console.log('Professors:', this.state.classProfs);
//     // console.log('Credits:', this.state.classCredits);
//     this.postDataToBackend();
//   }

//   setClassNames = (array2D) => {
//     const newNames = [];
//     for (let i = 0; i < array2D.length; i++) {
//       newNames.push(array2D[i][0]);
//     }
//     this.setState({ classNames: newNames });
//   }

//   componentDidMount() {
//     this.getDataFromBackend();
//   }

//   render() {
//     const { classNames } = this.state;
//     return (
//       <>
//         <head>
//           <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.3.1/dist/css/bootstrap.min.css" integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T" crossOrigin="anonymous"></link>
//         </head>

//         <h1>Almost there!</h1>
//         <p>We just need a little more information!</p>
//         <div className="input-areas-container">
//           {classNames.map((value, index) => (
//             <div key={index} className="input-group flex-nowrap">
//               <span className="input-group-text" id="addon-wrapping">
//                 {value}
//               </span>
//               <input
//                 type="text"
//                 className="form-control"
//                 placeholder="Professor"
//                 aria-label="Professor"
//                 aria-describedby="addon-wrapping"
//                 value={this.state.classProfs[index]}
//                 onChange={(event) => this.handleProfessorChange(index, event)}
//               />
//               <select className="form-select" aria-label="Select credits" onChange={(event) => this.handleCreditChange(index, event)}>
//                 <option value="1">1 Credit</option>
//                 <option value="2">2 Credits</option>
//                 <option value="3">3 Credits</option>
//                 <option value="4">4 Credits</option>
//               </select>
//             </div>
//           ))}
//           <button type="button" class="btn btn-outline-primary" onClick={this.handleSubmit}>Submit & Grade Schedule</button>
//         </div>
//       </>
//     );
//   }
// }

// export default withRouter(InputData);

import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";

const InputData = () => {
  const [classNames, setClassNames] = useState([]);
  const [classProfs, setClassProfs] = useState(Array(5).fill(''));
  const [classCredits, setClassCredits] = useState(Array(5).fill(1));
  const navigate = useNavigate();

  const getDataFromBackend = async () => {
    const response = await fetch('http://127.0.0.1:5000/api/input');
    const data = await response.json();
    setClassNames(data.map(item => item[0]));
  };

  const postDataToBackend = async () => {
    const data = {
      classes: [classNames, classProfs, classCredits]
    };

    try {
      const response = await fetch('http://127.0.0.1:5000/api/input', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
      });

      if (!response.ok) {
        throw new Error('Network response was not ok');
      }

      const result = await response.json();
      console.log(result);

      // Redirect after successful submission
      navigate('/output');
    } catch (error) {
      console.error('Error:', error);
    }
  };

  const handleProfessorChange = (index, event) => {
    const newProfs = [...classProfs];
    newProfs[index] = event.target.value;
    setClassProfs(newProfs);
  };

  const handleCreditChange = (index, event) => {
    const newCredits = [...classCredits];
    newCredits[index] = Number(event.target.value);
    setClassCredits(newCredits);
  };

  const handleSubmit = () => {
    postDataToBackend();
  };

  useEffect(() => {
    getDataFromBackend();
  }, []);

  return (
    <>
      <head>
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.3.1/dist/css/bootstrap.min.css" integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T" crossOrigin="anonymous"></link>
      </head>

      <h1>Almost there!</h1>
      <p>We just need a little more information!</p>
      <div className="input-areas-container">
        {classNames.map((value, index) => (
          <div key={index} className="input-group flex-nowrap">
            <span className="input-group-text" id="addon-wrapping">
              {value}
            </span>
            <input
              type="text"
              className="form-control"
              placeholder="Professor"
              aria-label="Professor"
              aria-describedby="addon-wrapping"
              value={classProfs[index]}
              onChange={(event) => handleProfessorChange(index, event)}
            />
            <select className="form-select" aria-label="Select credits" onChange={(event) => handleCreditChange(index, event)}>
              <option value="1">1 Credit</option>
              <option value="2">2 Credits</option>
              <option value="3">3 Credits</option>
              <option value="4">4 Credits</option>
            </select>
          </div>
        ))}
        <button type="button" className="btn btn-outline-primary" onClick={handleSubmit}>Submit & Grade Schedule</button>
      </div>
    </>
  );
};

export default InputData; // Export as a functional component
