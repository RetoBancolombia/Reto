import type {Metadata} from "next";
import {Inter} from "next/font/google";
import "./globals.css";
import React from "react";
import {Container, Nav, Navbar, NavbarBrand, NavLink} from "react-bootstrap";
import "react-datepicker/dist/react-datepicker.css";

const inter = Inter({subsets: ["latin"]});

export const metadata: Metadata = {
    title: "Create Next App",
    description: "Generated by create next app",
};

export default function RootLayout({
                                       children,
                                   }: Readonly<{
    children: React.ReactNode;
}>) {
    return (
        <html lang="en" data-bs-theme="dark">
            <body className={inter.className}>
            <Navbar bg="dark" expand="md">
                <Container>
                    <NavbarBrand>Reto Bancolombia</NavbarBrand>
                    <Nav className="me-auto">
                        <NavLink href="/">Home</NavLink>
                        <NavLink href="/commits">Commits</NavLink>
                        <NavLink href="/pipelines">Pipelines</NavLink>
                        <NavLink href="/pullrequests">Pull Requests</NavLink>
                        {/*<NavLink href="/repos">Repositories</NavLink>*/}
                    </Nav>
                </Container>
            </Navbar>
            <div className="container">
                {children}
            </div>
            </body>
        </html>
    );
}
