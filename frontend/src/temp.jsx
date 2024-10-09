import React, { useState, useEffect } from "react";
import axios from "axios";

function App() {
  const [board, setBoard] = useState([]);
  const [message, setMessage] = useState("");
  const [player, setPlayer] = useState("X");
  const [gameOver, setGameOver] = useState(false);
  const [makingMove, setMakingMove] = useState(false);
  const [choice, setChoice] = useState("");
  const [gameStart, setGameStart] = useState(false);
  const [user, setUser] = useState(null); // User object for authentication

  useEffect(() => {
    start();
  }, []);

  const start = () => {
    fetchBoard();
  };

  const fetchBoard = async () => {
    const response = await axios.get("http://localhost:8000/board");
    setBoard(response.data.board);
  };

  const aiMove = async () => {
    if (gameOver) {
      return;
    }
    const response = await axios.get("http://localhost:8000/ai");
    if (response.data != null) {
      const { move } = response.data;
      handleMove(move[0], move[1]);
    }
  };

  const handleMove = async (row, column) => {
    if (gameOver) {
      return;
    }
    const response = await axios.post("http://localhost:8000/move", {
      row,
      column,
    });
    if (response.data.status === "Game Over") {
      setGameOver(true);
      console.log(response.data.winner);
    }
    setBoard(response.data.board);
    setPlayer(response.data.player);
    setMessage(response.data.status);
  };

  const handleMoves = async (row, column) => {
    if (!makingMove) {
      setMakingMove(true);
      await handleMove(row, column);
      await aiMove();
      setMakingMove(false);
    }
  };

  const handleReset = async () => {
    const response = await axios.get("http://localhost:8000/reset");
    setBoard(response.data.board);
    setMessage("");
    setGameOver(false);
    setPlayer("X");
    setGameStart(false);
  };

  const handleLogin = () => {
    // Implement OAuth login logic here
    // Set the user object after successful login
    setUser({
      name: "John Doe",
      email: "john.doe@example.com",
      // Add more user properties as needed
    });
  };

  const handleLogout = () => {
    // Implement OAuth logout logic here
    // Clear the user object after successful logout
    setUser(null);
  };

  return (
    <>
      <div>
        <h1>Tic Tac Toe</h1>

        {!user ? (
          <button onClick={handleLogin}>Login</button>
        ) : (
          <>
            <button onClick={handleLogout}>Logout</button>
            {!gameStart ? (
              <>
                <button
                  onClick={() => {
                    setGameStart(true);
                    setChoice("X");
                  }}
                >
                  Play as X
                </button>
                <button
                  onClick={() => {
                    setGameStart(true);
                    setChoice("O");
                  }}
                >
                  Play as O
                </button>
              </>
            ) : (
              <>
                <div className="flex">
                  {!gameOver && (
                    <div>{player === "X" ? "X's turn" : "O's turn"}</div>
                  )}
                  {board.map((row, i) => (
                    <div key={i} style={{ display: "flex" }}>
                      {row.map((cell, j) => (
                        <div
                          key={j}
                          onClick={() => handleMoves(i, j)}
                          style={{
                            width: "50px",
                            height: "50px",
                            display: "flex",
                            justifyContent: "center",
                            alignItems: "center",
                            border: "1px solid black",
                          }}
                        >
                          {cell ? cell : "-"}
                        </div>
                      ))}
                    </div>
                  ))}
                </div>
                <p>{message}</p>
                <button onClick={handleReset}>Reset Game</button>
              </>
            )}
          </>
        )}
      </div>
    </>
  );
}

export default App;


