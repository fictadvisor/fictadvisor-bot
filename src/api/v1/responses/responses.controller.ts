import {ResponsesService} from "./responses.service";

export class ResponsesController {
  static async broadcastPending(req, res) {
    try {
      const data = await ResponsesService.broadcastPending(req.body);
      return res.status(200).send({message: data});
    } catch (err) {
      return res.status(400).send({message: 'An exception occurred while sending message'});
    }
  }
}