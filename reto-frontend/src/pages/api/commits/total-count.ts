import {NextApiRequest, NextApiResponse} from "next";
import database from "../../../../middleware/database";
import nextConnect, {createRouter} from "next-connect";
import {IncomingMessage} from "node:http";
// @ts-ignore
const router = createRouter<NextApiRequest, NextApiResponse>();


router.use(database)
    .get(async (req, res, next) => {
    if (req.query.from && req.query.to){
        const count = await req.db.collection("commits").countDocuments({
            timestamp: {
                $gte: new Date(String(req.query.from)),
                $lte: new Date(String(req.query.to))
            }
        })
        res.send(count)
    }else{
        const count = await req.db.collection("commits").countDocuments()
        res.send(count)
    }
})
export default router.handler()