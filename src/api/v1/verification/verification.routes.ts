import { Router } from 'express';
import { VerificationController } from './verification.controller';

const router = Router();

router.route('/verification/captain').post(VerificationController.verifyCaptain)
router.route('/verification/student').post(VerificationController.verifyStudent)

export default router;