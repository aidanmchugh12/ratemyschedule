import React, { useEffect, useState } from 'react';

function App() {
  const [message, setMessage] = useState('');

  // Fetch data from Flask when the component mounts
  useEffect(() => {
    fetch('http://127.0.0.1:5000/api/data')
      .then(response => response.json())
      .then(data => setMessage(data.message));
  }, []);

  // Submit data to Flask
  const submitData = async () => {
    const response = await fetch('http://127.0.0.1:5000/api/submit', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ text: 'Hello Flask from React!' }),
    });

    const result = await response.json();
    console.log(result);
  };

  return (
    <div>
      {/* <h1>{message}</h1> */}
      <h1>RateMySchedule!</h1>
      <p>Attatch .ics file below to analyze your schedule!</p>
      <button onClick={submitData}>Submit Data</button>
    </div>
  );
}

export default App;

