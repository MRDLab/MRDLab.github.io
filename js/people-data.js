/* =============================================================================
   MRD LAB — PEOPLE ROSTER
   =============================================================================
   This is the only file you need to edit to update the People page.

   TO ADD SOMEONE
   --------------
   1. Drop their photo in  images/people/   (square crops look best, ~600x600).
   2. Add an entry to the right group below. Copy an existing line and edit it.

   FIELDS
   ------
   name    (required)  Full name as it should display.
   role    (required)  Title shown under the name.
   photo               Filename inside images/people/. Omit it (or leave "")
                       and a maroon tile with their initials appears instead,
                       so nothing looks broken while you collect photos.
   blurb               One or two sentences. Optional.
   email               Just the address, e.g. "timk@umn.edu". Optional.
   links               Extra links: [{ label: "Google Scholar", url: "..." }]

   ALUMNI get a simpler shape:  { name: "...", degree: "Ph.D. 2024" }

   NOTE: entries marked  // TODO  are placeholders — replace them with the
   lab's current members.
   ========================================================================== */

window.MRD = window.MRD || {};

window.MRD.people = {

  /* ---------------------------------------------------------- lead faculty */
  lead: {
    name:  'Timothy M. Kowalewski, Ph.D.',
    role:  'Lead Faculty / Principal Investigator',
    photo: 'tim-kowalewski.jpg',
    email: 'timk@umn.edu',
    blurb: 'Dr. Kowalewski directs the Medical Robotics and Devices Lab in the ' +
           'Department of Mechanical Engineering at the University of Minnesota. ' +
           'His research advances the emerging field of computational surgery — ' +
           'the fusion of signal processing, controls, cyber-physical systems, ' +
           'and pervasive instrumentation applied to surgical robotics, medical ' +
           'devices, and simulation.',
    links: [
      { label: 'Email', url: 'mailto:timk@umn.edu' }
    ]
  },

  /* --------------------------------------------------------------- groups
     Each group renders as a titled section of photo cards, in this order.
     Delete a group you do not need; add one by copying the shape.          */
  groups: [
    {
      title: 'Staff',
      members: [
        // TODO — replace with current lab staff
        {
          name:  'Lab Coordinator',
          role:  'Lab Coordinator',
          photo: '',
          blurb: 'Placeholder — add the current lab coordinator here.'
        }
      ]
    },

    {
      title: 'Doctoral Students',
      members: [
        // TODO — replace these with the lab's current Ph.D. students
        {
          name:  'Doctoral Student',
          role:  'Doctoral Student',
          photo: '',
          blurb: 'Placeholder — copy this block once per current student.'
        }
      ]
    },

    {
      title: "Master's Students",
      members: [
        // TODO — replace with current master's students
        {
          name:  "Master's Student",
          role:  "Master's Student",
          photo: '',
          blurb: 'Placeholder.'
        }
      ]
    },

    {
      title: 'Undergraduate Researchers',
      members: [
        // TODO — replace with current undergraduate researchers
        {
          name:  'Undergraduate Researcher',
          role:  'Undergraduate Researcher',
          photo: '',
          blurb: 'Placeholder.'
        }
      ]
    }
  ],

  /* --------------------------------------------------------------- alumni
     Everyone who has graduated. Newest first.
     Entries with an empty degree string still render — fill in the year when
     you have it.                                                            */
  alumni: [
    // Recently graduated — previously listed as current members.
    // Degrees below are from the lab's recollection and still need graduation
    // years; the master's and undergraduate degrees in particular were given
    // as "I think", so confirm them before treating this as authoritative.

    // Ph.D., Mechanical Engineering
    { name: 'Chaitanya Awasthi',   degree: 'Ph.D. Mechanical Engineering' },
    { name: 'Yusra Farhat Ullah',  degree: 'Ph.D. Mechanical Engineering' },
    { name: 'Travis Beckerle',     degree: 'Ph.D. Mechanical Engineering' },
    { name: 'Nate Davies',         degree: 'Ph.D. Mechanical Engineering' },
    { name: 'Mandi Lye',           degree: 'Ph.D. Mechanical Engineering' },
    { name: 'Matthew Kubala',      degree: 'Ph.D. Mechanical Engineering' },
    { name: 'Adarsh Somayaji',     degree: 'Ph.D. Mechanical Engineering' },

    // Master's — Minnesota Robotics Institute (MnRI)
    { name: 'Emily Goldberg',      degree: 'M.S. Robotics (MnRI)' },
    { name: 'Aditya Koratkar',     degree: 'M.S. Robotics (MnRI)' },
    { name: 'Sarah Hanson',        degree: 'M.S. Robotics (MnRI)' },
    { name: 'Faizan Malik',        degree: 'M.S. Robotics (MnRI)' },

    // Undergraduate
    { name: 'Charles Feng',        degree: 'B.S. Mechanical Engineering' },
    { name: 'Khoi Nguyen',         degree: 'B.S. Computer Science' },

    // Staff
    { name: 'Bradley Drahos',      degree: 'Lab Coordinator' },

    // Previously listed alumni, with degrees on record.
    { name: 'Orla Gotthelf',       degree: 'Ph.D. 2024' },
    { name: 'Gillian McDonald',    degree: 'Ph.D. 2021' },
    { name: 'Ben Hamlen',          degree: 'B.S.M.E. 2020' },
    { name: 'Rebecca Smith',       degree: 'Ph.D. 2020' },
    { name: 'Jason Kelly',         degree: 'Ph.D. 2020' },
    { name: 'Bin Fu',              degree: 'M.S. 2020' },
    { name: 'Mark Gilbertson',     degree: 'Ph.D. 2019' },
    { name: 'Amer Safdari',        degree: 'M.S. 2019' },
    { name: 'Trevor Stephens',     degree: 'Ph.D. 2019' },
    { name: 'Catherine Ling',      degree: 'M.S.M.E. 2019' },
    { name: 'Anna French',         degree: 'Ph.D. 2018' },
    { name: 'Darrin Beekman',      degree: 'Ph.D. 2017' },
    { name: "John O'Neill",        degree: 'Ph.D. 2017' },
    { name: 'Rodney Dockter',      degree: 'Ph.D. 2017' },
    { name: 'Alex Win',            degree: 'M.S.M.E. 2015' },
    { name: 'Cory Schaffhausen',   degree: 'Ph.D. 2015' },
    { name: 'Sachin Bijadi',       degree: 'M.S.M.E. 2014' },
    { name: 'Kevin Ruda',          degree: 'M.S.M.E. 2014' },
    { name: 'Michael Winek',       degree: 'M.S.M.E. 2014' },
    { name: 'Jalal Rana',          degree: 'M.S.M.E. 2013' },
    { name: 'Astrini Sie',         degree: 'M.S.M.E. 2013' }
  ]
};
