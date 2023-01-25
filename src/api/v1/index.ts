import {Router} from 'express';
import CaptainsRoutes from "./captains/captains.routes";
import StudentsRoutes from "./students/students.routes";
import SuperheroesRoutes from "./superheroes/superheroes.routes";

const router = Router();

router.use('/captains', CaptainsRoutes);
router.use('/students', StudentsRoutes);
router.use('/superheroes', SuperheroesRoutes);


export default router;