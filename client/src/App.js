<<<<<<< HEAD
import "./App.css";
import Routers from "./routes/Routers";
function App() {
  return (
    <div>
      <Routers />
    </div>
  );
}

export default App;
=======
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
>>>>>>> 711d23f0695cc59924091f4e24b9b0fcd395aa50
