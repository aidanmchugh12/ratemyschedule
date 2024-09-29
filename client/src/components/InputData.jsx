import React from "react";

class InputData extends React.Component {
  constructor() {
    super();

    this.state = {
      classNames: [],
      classProfs: [],
      classCredits: [1, 1, 1, 1, 1],
    };
  }

  getDataFromBackend = async () => {
    const response = await fetch('http://127.0.0.1:5000/api/test');
    const data = await response.json();
    this.setClassNames(data);
  };

  testData = [
    ["T 001", "loc1", "name1", "day", "start", "end", "", ""],
    ["T 002", "loc1", "name1", "day", "start", "end", "", ""],
    ["T 003", "loc1", "name1", "day", "start", "end", "", ""],
    ["T 004", "loc1", "name1", "day", "start", "end", "", ""],
    ["T 005", "loc1", "name1", "day", "start", "end", "", ""],
  ];

  setClassNames = (array2D) => {
    const newNames = [];
    for (let i = 0; i < array2D.length; i++) {
      newNames.push(array2D[i][0]);
    }
    this.setState({ classNames: newNames });
  }

  componentDidMount() {
    this.getDataFromBackend();
  }

  render() {
    const { classNames } = this.state;
    return (
      <>
        <head>
          <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.3.1/dist/css/bootstrap.min.css" integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T" crossorigin="anonymous"></link>
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
              />
              <select className="form-select" aria-label="Select credits">
                <option value="1">1 Credit</option>
                <option value="2">2 Credits</option>
                <option value="3">3 Credits</option>
                <option value="4">4 Credits</option>
              </select>
            </div>
          ))}
          <button type="button" class="btn btn-outline-primary">Submit & Grade Schedule</button>
        </div>
      </>
    );
  }
}

export default InputData;