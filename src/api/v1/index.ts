import { Router } from "express";
import TeachersRoutes from "./teachers/teachers.routes";

const router = Router();

router.use("/teachers", TeachersRoutes)

export default router;