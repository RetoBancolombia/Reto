'use client'

import DatePicker from "react-datepicker";
import {useEffect, useState} from "react";
import {Form, FormCheck} from "react-bootstrap";

export default function PullRequests() {
    const [numberPRs, setNumberPRs] = useState(null)
    const [isOpened, setIsOpened] = useState(true)
    const [fromDate, setFromDate] = useState(new Date("2020-01-01T05:00:01Z"))
    const [toDate, setToDate] = useState(new Date())


    function updatePRs() {
        fetch("/api/pull-requests/total-count?" + new URLSearchParams({
            from: fromDate.toISOString(),
            to: toDate.toISOString(),
            open: String(isOpened)
        }))
            .then((res) => res.json())
            .then((data) => {
                setNumberPRs(data)
            })
    }

    useEffect(() => {
        updatePRs();
    }, [fromDate, toDate, isOpened]);
    return (
        <div>

            <h1>Pull requests</h1>
            <Form>
                <div className="mb-3">
                    <FormCheck
                        type="radio"
                        label="Opened pull requests"
                        checked={isOpened}
                        onChange={_ => setIsOpened(true)}
                    />
                    <FormCheck
                        type="radio"
                        label="Closed pull requests"
                        checked={!isOpened}
                        onChange={_ => setIsOpened(false)}
                    />
                </div>
            </Form>
            <p>Across all repositories, there were {numberPRs} pull requests found that
                were {isOpened ? "opened" : "closed"} within the given time period.</p>
            <p></p>
            <form>
                <legend>Pull requests {isOpened ? "opened" : "closed"} with a given time period</legend>
                <div className="mb-3">
                    <label>From: </label>
                    <DatePicker
                        selected={fromDate}
                        onChange={setFromDate}
                        selectsStart
                        showTimeSelect
                        dateFormat="Pp"
                    />
                </div>
                <div className="mb-3">
                    <label>To: </label>
                    <DatePicker
                        selected={toDate}
                        onChange={setToDate}
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