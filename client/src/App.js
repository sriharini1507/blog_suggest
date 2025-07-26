import React, { useState } from "react";
import axios from "axios";

function App() {
  const [url, setUrl] = useState("");
  const [ideas, setIdeas] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleAnalyze = async () => {
    if (!url) {
      setError("Please enter a website URL.");
      return;
    }

    setLoading(true);
    setIdeas("");
    setError("");

    try {
      const response = await axios.post("http://127.0.0.1:5000/analyze", {
        url,
      });

      if (response.data.blog_ideas) {
        setIdeas(response.data.blog_ideas);
      } else {
        setError("No blog ideas returned. Try another site.");
      }
    } catch (err) {
      console.log("Error:", err);
      setError("Error contacting backend. Make sure Flask is running.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ padding: "2rem", fontFamily: "Arial", maxWidth: "600px", margin: "0 auto" }}>
      <h1>🧠 Blog Suggestor</h1>
      <p>Enter a website URL to get blog topic ideas powered by AI!</p>

      <input
        type="text"
        value={url}
        onChange={(e) => setUrl(e.target.value)}
        placeholder="e.g. https://example.com"
        style={{ width: "100%", padding: "10px", marginTop: "10px" }}
      />
      <button
        onClick={handleAnalyze}
        style={{
          marginTop: "10px",
          padding: "10px 20px",
          backgroundColor: "#4CAF50",
          color: "white",
          border: "none",
          cursor: "pointer",
        }}
      >
        Analyze Website
      </button>

      {loading && <p>⏳ Generating blog ideas...</p>}
      {error && <p style={{ color: "red" }}>{error}</p>}

      {ideas && (
        <div style={{ marginTop: "20px", whiteSpace: "pre-wrap" }}>
          <h3>📝 Suggested Blog Ideas:</h3>
          <p>{ideas}</p>
        </div>
      )}
    </div>
  );
}

export default App;
