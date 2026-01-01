---
layout: default
title: Cryptographic hash
lang: en
permalink: /en/concepts/cryptographic-hash/
---

A **cryptographic hash** is a mathematical function that converts any amount of data (text, file, thesis) into a fixed-length unique "fingerprint" (here: 64 characters using SHA-256).

**Key properties:**
- **Unique**: even a single space or period difference produces a completely different hash.
- **Irreversible**: you can never reconstruct the original text from the hash.
- **Deterministic**: the same input always produces the same hash.
- **Fast**: hashing an entire thesis takes milliseconds.

**Why do we use hashes in the Open Internet Manifest?**
- Every thesis, guide, and concept has an official hash.
- You as a reader can copy the text, hash it yourself (with SHA-256), and compare it to the official hash.
- Does it match? Then you know with 100% certainty you're reading the authentic, unaltered version.
- If anyone (even the maintainer) changes a single letter? The hash no longer matches → change immediately visible.

The hashes make the manifest **decentrally verifiable**: no need to trust a central source, only mathematics.

> "A hash is digital sealing wax: break it, and everyone sees it."  
> — Ruben Berkhout