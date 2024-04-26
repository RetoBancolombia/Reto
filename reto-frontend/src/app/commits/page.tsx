'use client'

import DatePicker from "react-datepicker";
import {useEffect, useState} from "react";

export default function Commits() {
    const [numberCommits, setNumberCommits] = useState(null)
    const [fromDate, setFromDate] = useState(new Date("2020-01-01T05:00:01Z"))
    const [toDate, setToDate] = useState(new Date())


    function updateCommits() {
        fetch("/api/commits/total-count?" + new URLSearchParams({
            from: fromDate.toISOString(),
            to: toDate.toISOString()
        }))
            .then((res) => res.json())
            .then((data) => {
                setNumberCommits(data)
            })
    }

    useEffect(() => {
        updateCommits();
    }, [fromDate, toDate]);
    return (
        <div>
            {
                numberCommits === null ? <>
                    <h1>Loading...</h1>
                    <p>Loading...</p>
                </> : <>
                    <h1>{`${numberCommits} commits in total`}</h1>
                    <p>Across all repositories, there were {numberCommits} commits found within the given time
                        period</p>
                </>
            }
            <p></p>
            <form>
                <div className="mb-3">
                    <label>From: </label>
                    <DatePicker
                        selected={fromDate}
                        onChange={(date) => setFromDate(date!)}
                        selectsStart
                        showTimeSelect
                        dateFormat="Pp"
                    />
                </div>
                <div className="mb-3">
                    <label>To: </label>
                    <DatePicker
                        selected={toDate}
                        onChange={(date) => setToDate(date!)}
                        selectsStart
                        showTimeSelect
                        minDate={fromDate}
                        dateFormat="Pp"
                    />
                </div>
            </form>
        </div>
    );
}