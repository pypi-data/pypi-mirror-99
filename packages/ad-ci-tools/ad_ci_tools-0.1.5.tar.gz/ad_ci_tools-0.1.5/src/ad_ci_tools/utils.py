from git import Repo


class JenkinsRepo(Repo):
    def get_git_data(self):
        """
        Return git repo data.
        In case of branch retun {branch: _name_}
        In case of pr return {pull_request: _number_}
        """

        name = self.git.name_rev("--name-only", "HEAD")
        # posible outputs
        ## local cloned
        # feature/ADH-1376/ADH-1377 #  branches
        # tags/0.1.4 #  tags
        ## jenkins cloned
        # remotes/origin/feature/ADH-1376/ADH-1378 #   branches
        # origin/pr/231/head #  pull requests
        # tags/0.1.4 #  tags

        reponame = self.remotes.origin.url.split("/")[-1].split(".git")[0]
        repoowner = self.remotes.origin.url.split("/")[-2].split(".com:")[-1]

        data = {"reponame": reponame, "repoowner": repoowner}
        # pull request case
        # it works basically on ci with
        # clean git init and fetch remote with +refs/pull/*:refs/origin/pr/*
        # in onther cases with high chance it wont detect pr
        if name.startswith("origin/pr/"):
            data.update({"pull_request": name.split("/")[2]})
            return data

        # tags case
        if name.startswith("tags/"):
            branch = [
                n
                for n in self.git.branch("-a", "--contains", name).splitlines()
                if "origin" in n
            ][0].split("/")[2]
        # all others case
        else:
            if name.startswith("remotes/origin/"):
                branch = name[len("remotes/origin/") :]
            else:
                branch = name

        data.update({"branch": branch})
        return data
