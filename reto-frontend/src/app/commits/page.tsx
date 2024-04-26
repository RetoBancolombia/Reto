'use client'
import styles from "@/app/page.module.css";
import {useEffect, useState} from "react";
export default function Commits() {
    const [numberCommits, setNumberCommits] = useState(null)

    // useEffect()
    return (
        <div>
            {
                numberCommits === null ? <>
                    <h1>"Loading..."</h1>
                    <p>Loading...</p>
                </>:<>
                    <h1>{`${numberCommits} commits in total`}</h1>
                    <p>Across all repositories, there were ${numberCommits} commits found</p>
                </>
            }


        </div>
    );
}