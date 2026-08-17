/**
 * RepoCard
 *
 * Displays a single repository entry.
 * Props:
 *   repo — { id, name, owner, description, language, stars, url }
 */
export default function RepoCard({ repo }) {
  return (
    <div className="repo-card">
      <div className="repo-card__title">
        <a href={repo.url} target="_blank" rel="noreferrer">
          {repo.owner}/{repo.name}
        </a>
      </div>

      <p className="repo-card__desc">{repo.description}</p>

      <div className="repo-card__meta">
        <span className="lang-tag">{repo.language}</span>
        <span className="stars">★ {repo.stars.toLocaleString()}</span>
      </div>
    </div>
  );
}
