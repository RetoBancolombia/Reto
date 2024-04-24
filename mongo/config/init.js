db = db.getSiblingDB('reto')
db.createUser(
    {
        user: "root",
        pwd: "root",
        roles: [
            {
                role: "readWrite",
                db: "reto"
            }
        ]
    }
);
db.createCollection('commits', { capped: false });
db.createCollection('pipelines', { capped: false });
db.createCollection('pullrequests', { capped: false });
db.createCollection('repositories', { capped: false });