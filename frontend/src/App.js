import React, { useState } from 'react';
import axios from 'axios';
import 'bootstrap/dist/css/bootstrap.min.css';

function App() {
  const [data, setData] = useState([]);
  const [tableType, setTableType] = useState('');
  const [page, setPage] = useState(1);
  const size = 5; 

  const fetchData = async (type) => {
    try {
      //clear old data first
      setData([]);
  
      //set new table type
      setTableType(type);
  
      // reset to first page
      setPage(1);
  
      //fetch new data
      const response = await axios.get(`http://127.0.0.1:5000/${type}?page=1&size=${size}`);
  
      setData(response.data);
    } catch (error) {
      console.error('Error fetching data:', error);
    }
  };
 

  const renderTable = () => {
    if (data.length === 0) {
      return <p>No data to display. Click a button above to fetch data.</p>;
    }
  
    let columns = [];
    if (tableType === 'breeds') {
      columns = ['Name', 'ID'];
    } else if (tableType === 'groups') {
      columns = ['Name', 'ID'];
    } else if (tableType === 'facts') {
      columns = ['Fact'];  //only 1 column
    }
  
    return (
      <>
        <table className="table table-bordered mt-3">
          <thead>
            <tr>
              {columns.map((col, idx) => (
                <th key={idx}>{col}</th>
              ))}
            </tr>
          </thead>
          <tbody>
            {data.map((item, index) => {
              if (tableType === 'breeds' || tableType === 'groups') {
                return (
                  <tr key={index}>
                    <td>{item.name}</td>
                    <td>{item.id}</td>
                  </tr>
                );
              } else if (tableType === 'facts') {
                return (
                  <tr key={index}>
                    <td>{item}</td>  
                  </tr>
                );
              } else {
                return null;
              }
            })}
          </tbody>
        </table>
  
        <div>
          <p>Showing page {page}, size {size}</p>
        </div>
      </>
    );
  };

  return (
    <div className="container mt-4">
      <h1>Dog API Viewer</h1>
      <div className="mb-3">
        <button className="btn btn-primary me-2" onClick={() => fetchData('breeds')}>
          Breeds
        </button>
        <button className="btn btn-primary me-2" onClick={() => fetchData('groups')}>
          Groups
        </button>
        <button className="btn btn-primary" onClick={() => fetchData('facts')}>
          Facts
        </button>
      </div>

      {renderTable()}
    </div>
  );
}

export default App;