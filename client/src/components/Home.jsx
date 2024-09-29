import React, { useState } from 'react';
import { useNavigate  } from 'react-router-dom';
import './home.css'

export default function Home() {
  const [file, setFile] = useState(null);
  const navigate = useNavigate();

  const submitData = async () => {
    if (!file) {
      console.error('No file selected');
      return;
    }

    const formData = new FormData();
    formData.append('file', file);

    const response = await fetch('http://127.0.0.1:5000/api/submit', {
      method: 'POST',
      body: formData,
    });

    const result = await response.json();
    navigate('/input');
  };

  return (
    <>
      <h1 class="title">RateMySchedule!</h1>
      <p>Attatch .ics file below to analyze your schedule!</p>
      <img class="photo" src="ICS_TO_CSV.png"></img>
      <div>
      <input
        type="file"
        onChange={(event) => setFile(event.target.files[0])}
      />
      <input
        accept=".ics"
        type="submit"
        onClick={submitData}
        value="Upload File"
      />
      </div>
    </>
  );
}
