import React from 'react'

class InputData extends React.Component {
  constructor() {
    super();

    this.state = {
      overallGrade: 'A',
      overallGradeBlurb: "efiugsadhkfjahk",
      classBreaks: 0,
      classBreaksBlurb: "",
      profRating: 0,
      profRatingBlurb: "",
      creditsTaken: 0,
      creditsTakenBlurb: "",
      loading: true,
      hasFetched: false,
    };
  }

  getDataFromBackend = async () => {
    if (this.state.hasFetched) return;
    try {
        const response = await fetch('http://127.0.0.1:5000/api/output');
  
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
  
        const data = await response.json();
        this.setState({
            overallGrade: data['overallGrade'],
            overallGradeBlurb: data['overallGradeBlurb'],
            classBreaks: data['classBreaks'],
            classBreaksBlurb: data['classBreaksBlurb'],
            profRating: data['profRating'],
            profRatingBlurb: data['profRatingBlurb'],
            creditsTaken: data['creditsTaken'],
            creditsTakenBlurb: data['creditsTakenBlurb'],
            loading: false,
            hasFetched: true,
        })

      } catch (err) {
        console.error('Error fetching grading results:', err);
      }
  }

  componentDidMount() {
    this.getDataFromBackend();
  }


  render() {
    const { overallGrade, overallGradeBlurb, classBreaks, classBreaksBlurb, profRating, profRatingBlurb, creditsTaken, creditsTakenBlurb, loading} = this.state;
    if (loading) {
        return (
          <div className="loading-screen">
            <h2>Loading...</h2>
            <p>Please wait while we gather your information.</p>
          </div>
        );
      }

    return (
      <>
      <head>
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.3.1/dist/css/bootstrap.min.css" integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T" crossOrigin="anonymous"></link>
      </head>
      <div class="overall-grade-container">
        <h1>{overallGrade}</h1>
        <p>{overallGradeBlurb}</p>
      </div>
      <div class="cards-container">
        <div class="card">
        <div class="card-header">
            <h5>Class Breaks: {classBreaks}/5</h5>
        </div>
        <div class="card-body">
            <p class="card-text">{classBreaksBlurb}</p>
        </div>

        <div class="card-header">
            <h5>Professor Rating: {profRating}/5</h5>
        </div>
        <div class="card-body">
            <p class="card-text">{profRatingBlurb}</p>
        </div>

        <div class="card-header">
            <h5>Credits: {creditsTaken}/5</h5>
        </div>
        <div class="card-body">
            <p class="card-text">{creditsTakenBlurb}</p>
        </div>
        </div>
      </div>
      </>
    );
  }
}

export default InputData;