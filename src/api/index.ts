import axios from 'axios'
import oauth from './oauth'
import reviews from './reviews'
import supeheroes from './supeheroes'
import teachers from './teachers'
import courses from './courses'
import subjects from './subjects'
import teacherContacts from './teacherContacts'

const client = axios.create({
  baseURL: process.env.API_BASE_URL,
  headers: { authorization: `Telegram ${process.env.BOT_TOKEN}` }
})

const api = {
  oauth: oauth(client),
  reviews: reviews(client),
  superheroes: supeheroes(client),
  teachers: teachers(client),
  courses: courses(client),
  subjects: subjects(client),
  contacts: teacherContacts(client)
}

export default api
