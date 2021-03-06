package com.overwhale.colibri_so.backend.entity;

import lombok.Data;
import org.hibernate.annotations.Type;

import javax.annotation.Nullable;
import javax.persistence.Entity;
import javax.persistence.EnumType;
import javax.persistence.Enumerated;
import javax.persistence.FetchType;
import javax.persistence.Id;
import javax.persistence.JoinColumn;
import javax.persistence.JoinTable;
import javax.persistence.ManyToMany;
import javax.persistence.Table;
import javax.validation.constraints.NotNull;
import java.time.OffsetDateTime;
import java.util.HashSet;
import java.util.Set;
import java.util.UUID;

@Entity
@Data
@Table(name = "snippets")
public class Snippet {
  @Id
  @Type(type = "uuid-char")
  @NotNull
  private UUID id;

  @NotNull private OffsetDateTime creationTime;

  @Nullable private OffsetDateTime lastChangedTime;

  @NotNull
  @Type(type = "uuid-char")
  private UUID creatorId;

  @Nullable private String content;

  @Nullable private String description;

  @Enumerated(EnumType.STRING)
  @NotNull
  private SnippetType snippetType;

  @Nullable private String mimetype;

  @Nullable private Integer favouriteLevel;

  @Nullable private String icon;

  @Nullable
  @ManyToMany(fetch = FetchType.EAGER)
  @JoinTable(
      name = "snippet_projects",
      joinColumns = {@JoinColumn(name = "snippetId", updatable = false, insertable = false)},
      inverseJoinColumns = {@JoinColumn(name = "projectId", updatable = false, insertable = false)})
  private Set<Project> projects = new HashSet<Project>();

  @Nullable
  @ManyToMany(fetch = FetchType.EAGER)
  @JoinTable(
      name = "snippet_tags",
      joinColumns = {@JoinColumn(name = "snippetId", updatable = false, insertable = false)},
      inverseJoinColumns = {@JoinColumn(name = "tagId", updatable = false, insertable = false)})
  private Set<Tag> tags = new HashSet<Tag>();

  @Nullable
  @ManyToMany(fetch = FetchType.EAGER)
  @JoinTable(
      name = "snippet_intents",
      joinColumns = {@JoinColumn(name = "snippetId", updatable = false, insertable = false)},
      inverseJoinColumns = {@JoinColumn(name = "intentId", updatable = false, insertable = false)})
  private Set<Intent> intents = new HashSet<Intent>();
}
