import axios from "axios";
import { useEffect, useState } from "react";

const App = () => {
  const [messages, setMessages] = useState([]);
  const [value, setValue] = useState("");

  useEffect(() => {
    const eventSource = new EventSource("http://localhost:8000/events/");
    eventSource.onmessage = function (event) {
      setMessages((prevMessages) => [...prevMessages, event.data]);
    };
    return () => {
      eventSource.close();
    };
  }, []);

  const addValue = async () => {
    await axios.post("http://localhost:8000/add-value/", { value });
    setValue("");
  };

  return (
    <div>
      <h1>Server-Sent Events</h1>
      <input
        type="text"
        value={value}
        onChange={(e) => setValue(e.target.value)}
        placeholder="Enter a value"
      />
      <button onClick={addValue}>Add Value</button>
      <ul>
        {messages.map((message, index) => (
          <li key={index}>{message}</li>
        ))}
      </ul>
    </div>
  );
};

export default App;
