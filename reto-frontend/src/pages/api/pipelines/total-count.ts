import {NextApiRequest, NextApiResponse} from "next";
import database from "../../../../middleware/database";
import {createRouter} from "next-connect";
// @ts-ignore
const router = createRouter<NextApiRequest, NextApiResponse>();

router.use(database)
    .get(async (req, res) => {
        const successful = req.query.successful === "true";
        let filter = {
            finished_at: {
                $gte: new Date(String(req.query.from)),
                $lte: new Date(String(req.query.to))
            },
            result: successful ? "succeeded" : "failed"
        }

        // @ts-ignore
        const count = await req.db.collection("pipelines").countDocuments(filter)
        res.send(count)
    })
export default router.handler()