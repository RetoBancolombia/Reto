import {NextApiRequest, NextApiResponse} from "next";
import database from "../../../../middleware/database";
import nextConnect, {createRouter} from "next-connect";
import {IncomingMessage} from "node:http";
// @ts-ignore
const router = createRouter<NextApiRequest, NextApiResponse>();

router.use(database)
    .get(async (req, res, next) => {
        const open = Boolean(req.query.open) ?? true;
        let filter;
        if (open){
            filter = {
                created_at: {
                    $gte: new Date(String(req.query.from)),
                    $lte: new Date(String(req.query.to))
                },
                action: "opened"
            };
        }else{
            filter = {
                closed_at: {
                    $gte: new Date(String(req.query.from)),
                    $lte: new Date(String(req.query.to))
                },
                action: "closed"
            }
        }
        const count = await req.db.collection("pullrequests").countDocuments(filter)
        res.send(count)
    })
export default router.handler()