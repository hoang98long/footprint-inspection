# Architecture Overview

The MVP keeps the AI pipeline in-process under the backend package to simplify local development. Module boundaries are explicit so compute-heavy stages can later become asynchronous workers or independently deployed AI services without changing public application layers.

PostgreSQL stores transactional metadata. Binary images and generated reports belong behind the `storage` abstraction; vector indexes belong behind `matching/retrieval`. Neither persistence implementation is defined by this skeleton.
