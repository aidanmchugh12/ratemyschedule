import React from 'react'

class InputData extends React.Component {
  constructor() {
    super();

    this.state = {
      overallGrade: 'A',
      overallGradeBlurb: "You did great!",
      classBreaks: 0,
      classBreaksBlurb: "this is testing",
      profRating: 0,
      profRatingBlurb: "",
      creditsTaken: 0,
      creditsTakenBlurb: "",
    };
  }

  getDataFromBackend = async () => {

  }

  componentDidMount() {
    this.getDataFromBackend();
  }

  render() {
    const { overallGrade, overallGradeBlurb, classBreaks, classBreaksBlurb } = this.state;
    return (
      <>
      <div class="overall-grade-container">
        <h1>{overallGrade}</h1>
        <p>{overallGradeBlurb}</p>
      </div>
      <div class="cards-container">
        <div class="breaks-card">
            <h1>{classBreaks}</h1>
            <p>{classBreaksBlurb}</p>
        </div>
      </div>
      </>
    );
  }
}

export default InputData;