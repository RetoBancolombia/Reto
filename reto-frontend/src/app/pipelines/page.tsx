'use client'
import {useEffect, useState} from "react";
import {Form, FormCheck} from "react-bootstrap";
import DatePicker from "react-datepicker";

export default function Pipelines() {
    const [numberPipelines, setNumberPipelines] = useState(null)
    const [isSuccessful, setIsSuccessful] = useState(true)
    const [fromDate, setFromDate] = useState(new Date("2020-01-01T05:00:01Z"))
    const [toDate, setToDate] = useState(new Date())


    function updatePipeliness() {
        fetch("/api/pipelines/total-count?" + new URLSearchParams({
            from: fromDate.toISOString(),
            to: toDate.toISOString(),
            successful: String(isSuccessful)
        }))
            .then((res) => res.json())
            .then((data) => {
                setNumberPipelines(data)
            })
    }

    useEffect(() => {
        updatePipeliness();
    }, [fromDate, toDate, isSuccessful]);
    return (
        <div>

            <h1>Completed pipelines</h1>
            <Form>
                <div className="mb-3">
                    <FormCheck
                        type="radio"
                        label="Successful pipeline executions"
                        checked={isSuccessful}
                        onChange={_ => setIsSuccessful(true)}
                    />
                    <FormCheck
                        type="radio"
                        label="Failed pipeline executions"
                        checked={!{isSuccessful}}
                        onChange={_ => setIsSuccessful(false)}
                    />
                </div>
            </Form>
            <p>Across all repositories, there were {numberPipelines} pipelines that completed {isSuccessful ?
                "successfully" : "unsuccessfully"} within the given time period.</p>
            <p></p>
            <form>
                <legend>Pipelines that completed {isSuccessful ? "successfully" : "unsuccessfully"} with a given time
                    period
                </legend>
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