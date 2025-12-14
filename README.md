# LifeLens
Transforming emotional memories into cinematic visual stories using structured, deterministic AI.

# Overview

LifeLens is an AI-powered storytelling tool that reconstructs meaningful human memories into cinematic visual scenes using Bria’s FIBO structured generation engine.
Users simply write a memory, and LifeLens translates it into:
Emotional metadata
1. A FIBO structured JSON prompt
2. A deterministic, reproducible AI-generated image

LifeLens was inspired by a personal tribute to my uncle — a doctor who dedicated his life to caring for others before passing too soon. This project is an attempt to preserve memories that matter… and help others do the same.

# What LifeLens Does

LifeLens converts your memory text into an interpretable, reproducible visual story by running a full structured pipeline:
Memory Text → Emotional Metadata → FIBO Structured Prompt → Deterministic Image
No prompt hacks.
No randomness.
Just clean, JSON-native storytelling powered by FIBO.

# Inspiration

LifeLens began with a memory of my uncle in his clinic — a moment I never captured in a photo but always wished I had. That longing inspired a question: “What if AI could help us see the memories we never got to capture?” LifeLens is a tribute to that idea — to the people and moments we carry with us.

#System Architecture

Frontend (React)
│
└──→ Backend (FastAPI)
      │
      ├──→ Emotional Metadata Extraction
      │
      └──→ FIBO /v2/image/generate
              │
              ├──→ Structured JSON Prompt
              ├──→ Deterministic Seed
              └──→ Image Render


# What’s Next for LifeLens

Memory library / timeline
Voice-based memory capture
Adjustable camera + lighting controls
Exportable “memory albums”
Tools for therapists + grief support
Structured JSON editing for advanced users
Integration with storyboarding & documentary workflows
LifeLens can grow into a powerful platform for preserving histories, legacies, and personal stories.
