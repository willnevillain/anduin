## How would you impement a ledger system, and how would this system be able to handle a situation where items are defective and a deal has to be reversed?
A ledger is in essence an append-only ordered list of transactions; an [event driven system](https://martinfowler.com/articles/201701-event-driven.html) is effectively the software equivalent to this.
At a high level, any side-effect / change of state that would occur we would capture as an event.
This system could handle reversing transactions by appending new events that invert the side effects from the original event (e.g. refunding any deducted funds, changing ownership of the weapon object, etc.).
An additional benefit of an event driven system is emitting events to be enqueued onto a message broker, such that other disparate systems can read and act on these events - very beneficial for modern microservice architectures.

## We want to start printing out a monthly aggregate rollup, with things like average acceptance rate per user class, going conversion rate between various weaponry types (this month, the rough market value of 1 staff is 3 swords). Walk through how you would design this system, and make it performant (caching strategy, etc.)
Currently, the backend of the system runs on a relational database. For one off questions (e.g. what was the market value of staves compared to swords in January 2019), all the transactions that occured in the desired time window could be pulled from the database to be modeled and analyzed. For a monthly aggregate rollup, a once-a-month cron job to run the queries for the questions and save the results for printing seems sufficiently performant.

There's opportunity for a more real-time system to provide quicker BI to the rest of the company.

A useful service to expose would be one that allows users to define the questions and build the queries that operate against our database; an in-house reporting and analytics tool.
Dashboards would be designable that allow viewing real time results of these queries. For real-time updating of data, we should store question query results in a cache (e.g. Redis) and only re-query the database on the expiry of a TTL.
Additionally, the database accessed should be a distinct `reporting` database from our production app database - this would prevent churn of heavy reporting queries from impacting performance of the platform.
An eventual-consistency paradigm of regularly (cadence defined by business need) copying updates from the app database to the reporting database would keep everything fairly up to date without being a drag on the overall system. 
