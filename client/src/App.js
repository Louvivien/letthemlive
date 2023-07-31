import React, { useState } from 'react';
import UserContext from "./context/UserContext";
import "./App.css";
import Routers from "./routes/Routers";
function App() {
  const [user, setUser] = useState(null);

  return (
    <UserContext.Provider value={{ user, setUser }}>

    <div>
      <Routers />
    </div>
    </UserContext.Provider>

  );
}

export default App;
