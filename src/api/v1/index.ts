import {Router} from 'express';
import CaptainsRoutes from "./captains/captains.routes";
import StudentsRoutes from "./students/students.routes";
import SuperheroesRoutes from "./superheroes/superheroes.routes";
import ResponsesRoutes from "./responses/responses.routes";

const router = Router();

router.use('/captains', CaptainsRoutes);
router.use('/students', StudentsRoutes);
router.use('/superheroes', SuperheroesRoutes);
router.use('/responses', ResponsesRoutes);


export default router;