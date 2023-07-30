import { useState } from "react";
import Calendarreact from "react-calendar";
import "react-calendar/dist/Calendar.css";
import "./Calendar.css"

const Calendar=()=> {
  const [date, setDate] = useState(new Date());
  return (
    <div className="app">
      <div className="calendar-container">
        <Calendarreact onChange={setDate} value={date} selectRange={false} />
      </div>
      {date.length > 0 ? (
        <p className="text-center">
          <span className="bold">Start:</span> {date[0].toDateString()}
          &nbsp;|&nbsp;
          <span className="bold">End:</span> {date[1].toDateString()}
        </p>
      ) : (
        // <p className="text-center">
        //   <span className="bold">Current Date:</span> {date.toDateString()}
        // </p>
        <></>
      )}
    </div>
  );
}

export default Calendar;