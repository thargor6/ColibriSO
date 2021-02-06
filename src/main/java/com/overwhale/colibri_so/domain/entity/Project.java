package com.overwhale.colibri_so.domain.entity;

import lombok.Data;
import org.hibernate.annotations.Type;

import javax.annotation.Nullable;
import javax.persistence.Entity;
import javax.persistence.Id;
import javax.persistence.Table;
import javax.validation.constraints.NotNull;
import java.time.OffsetDateTime;
import java.util.UUID;

@Entity
@Data
@Table(name = "projects")
public class Project {
  @Id
  @Type(type = "uuid-char")
  @Nullable
  private UUID id;

  @Nullable
  private OffsetDateTime creationTime;

  @Nullable
  private OffsetDateTime lastChangedTime;

  @Nullable
  private UUID creatorId;

  @NotNull
  private String project;

  @Nullable
  private String description;
}
