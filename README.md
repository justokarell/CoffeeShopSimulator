# CoffeeShopSimulator

## Goal
Optimization strategy for managing a coffee shop's operations to maximize throughput and minimize customer wait times. Specifically, we focus on determining the optimal thresholds (\(T_o\) and \(T_w\)) for switching roles between baristas to ensure that both the queue for taking orders and the waiting area for fulfilled orders remain within their respective capacities. By deriving these thresholds in terms of key operational parameters and validating them through simulation, we provide a robust framework for dynamic role management in the coffee shop setting.

## Description
M/M/s/n queueing simulation with a menu of Poisson-distributed arrival times.
\section{Problem Statement}
We aim to optimize the operations of a coffee shop with the following setup:
\begin{itemize}
    \item \textbf{Employees:}
    \begin{itemize}
        \item 1 cook who handles only food preparation.
        \item 2 baristas who can either take orders or make coffee, but not both simultaneously.
    \end{itemize}
    \item \textbf{Customer Orders:}
    \begin{itemize}
        \item Orders can be for coffee, food, or both.
        \item The order process involves two steps: taking the order and fulfilling the order.
    \end{itemize}
    \item \textbf{Queue and Waiting Area:}
    \begin{itemize}
        \item A single queue for taking orders.
        \item A waiting area with a finite capacity (\(C_w\)), where customers wait after placing their orders until they are fulfilled.
    \end{itemize}
\end{itemize}











