import React, { useState } from 'react';
import axios from 'axios';
import './App.css';
import Home from './pages/Home'

function App(){
  return <Home/>
}

// function App() {
//   const [predictions, setPredictions] = useState([]);

//   const handlePredictions = async () => {
//     try {
//       const response = await axios.get('http://127.0.0.1:5000/receive_predictions');
//       setPredictions(response.data);
//     } catch (error) {
//       console.error('Error fetching predictions:', error);
//     }
//   };

//   return (
//     <div className="App">
//       <button onClick={handlePredictions}>Get Predictions</button>
//       <div>
//         <h3>Predictions:</h3>
//         <ul>
//           {predictions.map((prediction, index) => (
//             <li key={index}>{prediction}</li>
//           ))}
//         </ul>
//       </div>
//     </div>
//   );
// }

export default App;
