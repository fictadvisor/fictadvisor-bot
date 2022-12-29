import { Router } from "express";
import TeachersRoutes from "./teachers.routes";

const router = Router();

router.use("/teachers", TeachersRoutes)

export default router;