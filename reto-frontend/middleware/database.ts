import { Db, MongoClient} from 'mongodb';
import nextConnect from 'next-connect';

const client = new MongoClient(process.env.MONGODB_URI ?? "mongodb://reto:Extrovert-Unbiased9-Oxidize-Recycler@localhost:27017/?authSource=reto", {
    // @ts-ignore
    useUnifiedTopology: true,
});

async function database(req: any, res: any, next: () => any) {
    req.dbClient = client;
    req.db = client.db('reto');
    return next();
}

// // @ts-ignore
// const middleware = nextConnect();
//
// middleware.use(database);

export default database;