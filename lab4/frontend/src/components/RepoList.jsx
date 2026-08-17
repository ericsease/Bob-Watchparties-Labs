import RepoCard from "./RepoCard";

/**
 * RepoList
 *
 * Renders the full list of trending repos.
 * Props:
 *   repos — array of repo objects
 */
export default function RepoList({ repos }) {
  if (!repos.length) {
    return <p className="state-message">No repos found.</p>;
  }

  return (
    <div className="repo-list">
      {repos.map((repo) => (
        <RepoCard key={repo.id} repo={repo} />
      ))}
    </div>
  );
}
