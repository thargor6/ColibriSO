package com.overwhale.colibri_so.domain.entity;

import lombok.Data;
import org.hibernate.annotations.Type;

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
  private UUID id;

  @NotNull
  private OffsetDateTime creationTime;

  private OffsetDateTime lastChangedTime;

  @NotNull
  private UUID creatorId;

  @NotNull private String project;

  private String description;
}
